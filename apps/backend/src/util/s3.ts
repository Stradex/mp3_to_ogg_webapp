import * as AWS from 'aws-sdk';

const createDigitalSpacesBucket = (endpoint: string, keyId: string, secret: string) => {
	return new AWS.S3({
    s3ForcePathStyle: false,
    endpoint: endpoint,
    region: "us-east-1",
		accessKeyId: keyId,
		secretAccessKey: secret,
    credentials: {
      accessKeyId: keyId,
      secretAccessKey: secret
    }
	});
}

export { createDigitalSpacesBucket };

