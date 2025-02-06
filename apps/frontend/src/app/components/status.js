'use client';
import Image from "next/image";
import UploadForm from '../components/upload.js';
import Link from 'next/link'
import { useState, useEffect } from 'react';

export default function FileStatus() {
	const [status, setStatus] = useState('undefined');
	const [downloadReady, setDownloadReady] = useState(false);
	const [fileID, setFileID] = useState('');

	useEffect(() => {
		const params = new Proxy(new URLSearchParams(window.location.search), {
			get: (searchParams, prop) => searchParams.get(prop),
		});
		const file_id = params.file;

    const getStatusData = async (id) => {
			try {
				const apiRes = await fetch(`/backend/status/${id}`, { method: 'GET'});
				const dataRes = await apiRes.json();
				setStatus(dataRes.status);
				setDownloadReady(dataRes.status === 'CONVERTED');

				setFileID(id);
			} catch (e) {
				setStatus('error');
			}
    }
    const updateStatus = setInterval(() => {
      getStatusData(file_id)
    }, 2*1000);
    return () => clearInterval(updateStatus);
  },[]);

  return (
			<div>
				<h2> Processing status: { status }</h2>
				{ downloadReady &&
					<Link href={`/download/?file=${fileID}`}>DOWNLOAD CONVERTED SOUND</Link>
				}
			</div>
  );
}

