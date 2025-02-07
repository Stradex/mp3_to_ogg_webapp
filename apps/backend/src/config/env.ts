import {
    EnvStorageType,
		EnvFileManagerType,
		EnvDigitalSpacesType
} from './env.d';
import fs from 'fs';
const dotenv = require('dotenv');
dotenv.config({ override: true });

export default () => ({
    storage: {
        host: process.env.STORAGE_HOST,
        isLocal: process.env.STORAGE_LOCAL === "true",
    } as EnvStorageType,
    file_manager: {
        host: process.env.FILE_MANAGER_HOST,
    } as EnvFileManagerType,
    spaces: {
        key_name: process.env.SPACES_KEY_NAME,
        access_id: process.env.SPACES_KEY_ID,
        access_key: process.env.SPACES_KEY,
				bucket_name: process.env.SPACES_BUCKET,
				endpoint: process.env.SPACES_ENDPOINT,
    } as EnvDigitalSpacesType,
});

