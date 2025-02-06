import 'dotenv/config';
import {
    EnvStorageType
} from './env.d';

export default () => ({
    storage: {
        host: process.env.STORAGE_HOST,
    } as EnvStorageType
});

