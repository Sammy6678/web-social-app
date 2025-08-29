import React, {useState} from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_BASE || 'https://<BACKEND_HOST>'

export default function PostForm({userId, onPosted}){
  const [caption, setCaption] = useState('')
  const [file, setFile] = useState(null)
  async function submit(e){
    e.preventDefault()
    const fd = new FormData()
    fd.append('user_id', userId)
    fd.append('caption', caption)
    if(file) fd.append('image', file)
    try{
      await axios.post(`${API}/post`, fd, { headers: {'Content-Type':'multipart/form-data'} })
      setCaption(''); setFile(null)
      onPosted && onPosted()
    }catch(err){
      alert('Post failed')
    }
  }
  return (
    <form onSubmit={submit} style={{marginBottom:20}}>
      <input type="file" onChange={e=>setFile(e.target.files[0])} />
      <input placeholder="Caption" value={caption} onChange={e=>setCaption(e.target.value)} style={{width:'100%',padding:8,margin:'8px 0'}} />
      <button type="submit">Post</button>
    </form>
  )
}
