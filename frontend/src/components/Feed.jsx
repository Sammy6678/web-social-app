import React, {useEffect, useState} from 'react'
import axios from 'axios'
import PostForm from './PostForm'

const API = import.meta.env.VITE_API_BASE || 'https://<BACKEND_HOST>'

export default function Feed(){
  const [userId,setUserId] = useState(localStorage.getItem('userId') || '')
  const [posts,setPosts] = useState([])

  useEffect(()=>{ load() },[])
  async function load(){
    try{
      const res = await axios.get(`${API}/posts`)
      setPosts(res.data || [])
    }catch(e){ console.error(e) }
  }

  if(!userId) return <div style={{padding:20}}>Please login <a href="/">Login</a></div>

  return (
    <div style={{maxWidth:800, margin:'20px auto'}}>
      <h2>Langunana Feed</h2>
      <PostForm userId={userId} onPosted={load}/>
      <div>
        {posts.map(p => (
          <div key={p.id} style={{border:'1px solid #ddd',padding:10, marginBottom:10}}>
            {p.image_url && <img src={p.image_url} alt="post" style={{maxWidth:'100%'}}/>}
            <p>{p.caption}</p>
            <small>By user {p.user_id} at {p.created_at}</small>
          </div>
        ))}
      </div>
    </div>
  )
}
