import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { EnvStorageType, EnvFileManagerType } from './config/env.d';


@Injectable()
export class AppService {
  env;
  constructor(private readonly configService: ConfigService) {
    this.env = {
			storage: configService.get<EnvStorageType>('storage'),
			file_manager: configService.get<EnvFileManagerType>('file_manager'),
    };
  }

  getHello(): string {
    return 'Hello World!';
  }
}
