import { StreamableFile, Controller, UseInterceptors, Query, Param, Get, Post, Body, UploadedFile, HttpStatus, Res, FileTypeValidator, ParseFilePipe } from '@nestjs/common';
import { AppService } from './app.service';
import { FileInterceptor } from '@nestjs/platform-express';
import { Express, Response, Request } from 'express';
import { memoryStorage } from 'multer';
import * as path from 'path';
import crypto from 'crypto';

function generateUniqueFileID(file: Express.Multer.File): string {
  const reducedHash = crypto.createHash('sha256').update(file.buffer).digest('hex').substring(0, 5);
	return `${Date.now()}${reducedHash}`;
}

function generateUniqueFileName(file: Express.Multer.File, file_id: string): string {
  const fileBasename = path.parse(path.basename(file.originalname)).name;
  const fileExt = path.extname(path.basename(file.originalname));
  const fullFileName: string = `${file_id}-${fileBasename.substring(0, 32)}${fileExt}`;
  console.log(`[DEBUG] File path: ${fullFileName}`);
  return fullFileName;
}

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post('upload/')
  @UseInterceptors(FileInterceptor('file', {
    storage: memoryStorage()
  }))
  async uploadFileAndValidate(
    @UploadedFile(
      new ParseFilePipe({
        validators: [
          //SEE: https://gist.github.com/AshHeskes/6038140
          new FileTypeValidator({ fileType: /(audio\/mpeg|application\/octet-stream)/ }),
        ],
      }),
    ) file: Express.Multer.File,
  @Body() mp3FileDto: any,
  @Res() res: Response) {
		const fileID: string = generateUniqueFileID(file);
		console.log("[DEBUG] File uploaded", file)
		const remoteFileName: string = generateUniqueFileName(file, fileID);
		console.log("[DEBUG] Storate local: ", this.appService.env.storage.isLocal);
		if (this.appService.env.storage.isLocal) {
			const formData = new FormData();
			formData.append('file', new Blob([file.buffer]), file.originalname);
			const orderRes = await fetch(`${this.appService.env.storage.host}upload/${fileID}`, { method: 'POST', body: formData });
			const dataRes = await orderRes.json();

			console.log("[DEBUG] FAPI response: ", dataRes);
			res.status(HttpStatus.OK).json({status: 'OK', fileUploaded: remoteFileName, fileID: fileID});
		} else {
			const s3Res = await this.appService.uploadFile(file, remoteFileName);
			console.log("S3 RESPONSE: ", s3Res);
			if (s3Res?.Location !== 'undefined' && s3Res?.Key !== 'undefined' && s3Res?.ETag !== 'undefined') {
				res.status(HttpStatus.OK).json({status: 'OK', fileUploaded: s3Res.Key, fileID: fileID});
			} else {
				res.status(HttpStatus.OK).json({status: 'ERROR', description: 'failed to upload file to storage server.'});
			}	
		}
  }

  @Get('status/:file_id')
  async getFileStatus(@Param('file_id') fileID: string, @Res() res: Response) {
		const orderRes = await fetch(`${this.appService.env.file_manager.host}status/${fileID}`, { method: 'GET' });
		const dataRes = await orderRes.json();
		// HERE: Connect with FASTAPI to check file status.
    res.status(HttpStatus.OK).json(dataRes);
  }

  @Get('download/:file_id')
  async downloadConvertedFile(@Param('file_id') fileID: string, @Res() res: Response) {
		if (this.appService.env.storage.isLocal) {
			const file_res = await fetch(`${this.appService.env.storage.host}download/${fileID}`, { method: 'GET' });
			const file_blob = await file_res.blob()
			console.log(file_blob);
			const arrayBuffer = await file_blob.arrayBuffer();
			const file_buffer = Buffer.from(arrayBuffer);
			res.setHeader("Content-Type", "audio/mpeg; charset=binary"); // set content type and charset
			res.charset = "binary";
			res.status(HttpStatus.OK).send(file_buffer);
		} else {
			const s3FileURL: string | null = await this.appService.getConvertedFileURL(fileID);
			console.log("S3 FILE URL: ", s3FileURL);
			if (!s3FileURL) {
				res.status(HttpStatus.OK).json({status: 'ERROR', description: 'Remote file does not exists.'});
			} else {
				res.status(HttpStatus.OK).json({status: 'OK', url: s3FileURL});
			}
		}
  }
}
