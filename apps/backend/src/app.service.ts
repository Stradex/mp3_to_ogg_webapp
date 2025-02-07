import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { EnvStorageType, EnvFileManagerType, EnvDigitalSpacesType } from './config/env.d';
import { Req, Res } from '@nestjs/common';
import { createDigitalSpacesBucket } from './util/s3'


@Injectable()
export class AppService {
	AWS_S3_BUCKET;
	s3;
  env;
  constructor(private readonly configService: ConfigService) {
		const digitalSpaces: EnvDigitalSpacesType = configService.get<EnvDigitalSpacesType>('spaces') ;

		this.AWS_S3_BUCKET = digitalSpaces.bucket_name;
		this.s3 = createDigitalSpacesBucket(digitalSpaces.endpoint, digitalSpaces.access_id, digitalSpaces.access_key);
		console.log("S3 DATA: ", this.s3);
    this.env = {
			spaces: configService.get<EnvDigitalSpacesType>('spaces'),
			storage: configService.get<EnvStorageType>('storage'),
			file_manager: configService.get<EnvFileManagerType>('file_manager'),
    };
  }

	async getConvertedFileURL(fileID) {
		const filesMatching = (await this.s3.listObjects({
			Bucket: this.AWS_S3_BUCKET,
			Prefix: `converted/${fileID}`
		}).promise()).Contents;
		console.log("[DEBUG] files mataching: ", filesMatching);
		return filesMatching.length > 0 ? `${this.env.spaces.endpoint}/${this.env.spaces.bucket_name}/${filesMatching[0].Key}` : null;
	}

  async uploadFile(file, uploadFileName) {
    return await this.s3_upload(
      file.buffer,
      this.AWS_S3_BUCKET,
      uploadFileName,
      file.mimetype,
    );
  }

  async s3_upload(file, bucket, name, mimetype) {
    const params = {
      Bucket: bucket,
      Key: `upload/${String(name)}`,
      Body: file,
      ACL: 'public-read',
      ContentType: mimetype,
    };

    try {
      let s3Response = await this.s3.upload(params).promise();
      return s3Response;
    } catch (e) {
      console.log(e);
    }
		return "error";
  }

  getHello(): string {
    return 'Hello World!';
  }
}
