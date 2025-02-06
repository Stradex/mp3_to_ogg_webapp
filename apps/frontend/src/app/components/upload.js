'use client';
import Form from 'next/form'
import { useState, useEffect } from 'react';

export default function UploadForm() {
	const [status, setStatus] = useState({});

	async function handleSubmit(event){
		event.preventDefault();
    try {
			const fileData = event.currentTarget.elements.fileToSubmit.files[0];
			const formData = new FormData();
      formData.append('file', fileData);
      const orderRes = await fetch('/backend/upload/', { method: 'POST', body: formData });
      const dataRes = await orderRes.json();
			if (dataRes.status === 'ERROR') {
				setStatus({
					error: true,
					description: dataRes.description
				});
			} else {
				console.log(dataRes);
				const file_id = dataRes.fileID;
				location.replace("/processing?file=" + file_id);
			}
    } catch (e) {
			console.error("Something failed...", e);
			setStatus({
				error: true,
				description: "Request to backend failed."
			});
    }
	}
  return (
		<div>
		{
			status && status.error && <h2>ERROR: {status.description} </h2>
		}
    <Form formEncType="multipart/form-data" onSubmit={async (event) => await handleSubmit(event)}>
      {/* On submission, the input value will be appended to
          the URL, e.g. /search?query=abc */}
			<input id="fileToSubmit" name="file" type="file" />
      <button type="submit">Convert file to ogg</button>
    </Form>
		</div>
  )
}
