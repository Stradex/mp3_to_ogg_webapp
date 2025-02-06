import {
    EnvStorageType,
		EnvFileManagerType
} from './env.d';
import fs from 'fs';
const dotenv = require('dotenv');
dotenv.config({ override: true });

export default () => { 
		return ({
    storage: {
        host: process.env.STORAGE_HOST,
        isLocal: process.env.STORAGE_LOCAL === "true",
    } as EnvStorageType,
    file_manager: {
        host: process.env.FILE_MANAGER_HOST,
    } as EnvFileManagerType
});

};

