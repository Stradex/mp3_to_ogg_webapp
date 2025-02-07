'use client';
import Player from "@madzadev/audio-player";
import "@madzadev/audio-player/dist/index.css";
import { useState, useEffect } from 'react';
import Link from 'next/link'

export default function SoundPlayer() {
	const [track, setTrack] = useState(null);

	useEffect(() => {
		const params = new Proxy(new URLSearchParams(window.location.search), {
			get: (searchParams, prop) => searchParams.get(prop),
		});
		const file_id = params.file;

    const downloadAudio = async (id) => {
			try {
				const apiRes = await fetch(`/backend/download/${id}`, { method: 'GET'});
				let audioURL = "";

				if (1) {
					const audioData = await apiRes.json();
					console.log(audioData);
					audioURL = audioData.url;
				} else {
					const audioBlob = await apiRes.blob();
					const newBlob = new Blob([audioBlob], { type: "audio/ogg",  codecs: "opus" })
					audioURL = URL.createObjectURL(newBlob);
				}
				setTrack({
					url: audioURL,
					title: "Converted file",
					tags: ["converted"],
				});
			} catch (e) {
				setTrack(null);
				console.error("error: ", e);
			}
    }
		downloadAudio(file_id);
    return;
  },[]);

  return (
		<div>
			{	track && track.url &&
				<audio controls src={track.url}></audio>
			}
			{	track && track.url &&
				<Link href={track.url}>Download converted OGG</Link>
			}

		</div>
  );
}

