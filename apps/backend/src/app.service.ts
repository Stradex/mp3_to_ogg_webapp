import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { EnvStorageType } from './config/env.d';


@Injectable()
export class AppService {
  env;
  constructor(private readonly configService: ConfigService) {
    this.env = {
			storage: configService.get<EnvStorageType>('storage')
    };
  }

  getHello(): string {
    return 'Hello World!';
  }
}
