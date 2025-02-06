import 'dotenv/config';
import {
    EnvStorageType,
		EnvFileManagerType
} from './env.d';

export default () => ({
    storage: {
        host: process.env.STORAGE_HOST,
        isLocal: Boolean(process.env.STORAGE_LOCAL.toLowerCase() === 'true'),
    } as EnvStorageType,
    file_manager: {
        host: process.env.FILE_MANAGER_HOST,
    } as EnvFileManagerType
});

