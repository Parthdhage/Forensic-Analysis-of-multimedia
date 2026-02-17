

    import streamlit as st
    import hashlib
    import subprocess
    import os
    import tempfile
    import json
    from datetime import datetime
    from PIL import Image
    import ffmpeg

    st.set_page_config(page_title="Multimedia Forensic Analyzer", layout="wide")

    st.title("🎥 Multimedia Forensic Analyzer")
    st.markdown(
        """
        Upload any **audio, video, or music file** (MP4, MP3, WAV, MKV, MOV, etc.), and this tool will perform a forensic analysis.

        It extracts key forensic evidence:
        - 🔍 File metadata (codec, duration, bitrate, etc.)
        - 🧾 Embedded EXIF/container data
        - 🧠 Cryptographic file hashes (MD5, SHA1, SHA256)
        - ⚙️ File structure validation (via ffprobe)
        - 🧩 Optional thumbnail/frame preview for videos
        """
    )

    def save_temp(uploaded_file):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1])
        tmp.write(uploaded_file.getvalue())
        tmp.flush()
        tmp.close()
        return tmp.name

    def compute_hashes(file_path):
        hashes = {'MD5': None, 'SHA1': None, 'SHA256': None}
        with open(file_path, 'rb') as f:
            data = f.read()
            hashes['MD5'] = hashlib.md5(data).hexdigest()
            hashes['SHA1'] = hashlib.sha1(data).hexdigest()
            hashes['SHA256'] = hashlib.sha256(data).hexdigest()
        return hashes

    def ffprobe_metadata(path):
        cmd = ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-print_format", "json", path]
        try:
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            return json.loads(p.stdout)
        except Exception as e:
            return {"error": str(e)}

    def extract_thumbnail(video_path, out_path):
        try:
            (
                ffmpeg
                .input(video_path, ss=1)
                .output(out_path, vframes=1)
                .overwrite_output()
                .run(quiet=True)
            )
            return True
        except Exception:
            return False

    st.header("📁 Upload a Multimedia File for Forensic Analysis")
    uploaded_file = st.file_uploader("Upload a file", type=["mp4","mkv","avi","mov","mp3","wav","aac","flac","m4a"])

    if uploaded_file:
        with st.spinner("Analyzing file..."):
            path = save_temp(uploaded_file)
            st.success(f"File saved temporarily at {path}")

            st.subheader("🧠 Cryptographic Hashes")
            hashes = compute_hashes(path)
            st.json(hashes)

            st.subheader("🧾 ffprobe Metadata")
            meta = ffprobe_metadata(path)
            if 'error' in meta:
                st.error(f"Error retrieving metadata: {meta['error']}")
            else:
                format_info = meta.get('format', {})
                streams = meta.get('streams', [])

                st.markdown("### File Format Info")
                st.table({k: v for k, v in format_info.items() if k in ['filename','format_name','duration','size','bit_rate','tags']})

                st.markdown("### Stream Details")
                for i, stream in enumerate(streams):
                    st.write(f"**Stream {i+1}:** {stream.get('codec_type','unknown')} — {stream.get('codec_name','n/a')}")
                    st.json({k: v for k, v in stream.items() if k in ['codec_name','codec_type','width','height','duration','bit_rate','tags']})

            if any(s.get('codec_type') == 'video' for s in meta.get('streams', [])):
                st.subheader("🎞️ Video Frame Preview")
                out_thumb = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg').name
                if extract_thumbnail(path, out_thumb):
                    img = Image.open(out_thumb)
                    st.image(img, caption="Extracted Frame (1s mark)")
                else:
                    st.warning("Could not extract thumbnail.")
            st.markdown("---")
            st.header("📋 Forensic Summary")
            st.markdown(f"**Filename:** {uploaded_file.name}")
            st.markdown(f"**Filesize:** {os.path.getsize(path)/1024:.2f} KB")
            st.markdown(f"**Analyzed at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ")

            
            report = {
                'file': uploaded_file.name,
                'hashes': hashes,
                'metadata': meta,
                'analysis_time': datetime.now().isoformat()
            }
            st.download_button(
                label="⬇️ Download JSON Forensic Report",
                data=json.dumps(report, indent=4),
                file_name=f"forensic_report_{os.path.splitext(uploaded_file.name)[0]}.json",
                mime="application/json"
            )
    else:
        st.info("Please upload a media file to start forensic analysis.")


    st.markdown('---')