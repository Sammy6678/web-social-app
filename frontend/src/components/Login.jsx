import React, {useState} from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_BASE || 'https://<BACKEND_HOST>'

export default function Login(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  async function handle(e){
    e.preventDefault()
    try{
      const res = await axios.post(`${API}/signin`, { username, password })
      // store simple session id (for demo)
      localStorage.setItem('userId', res.data.user_id || res.data.userId || '')
      window.location.href = '/feed'
    }catch(err){
      alert(err?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div style={{maxWidth:420, margin:'40px auto', padding:20, border:'1px solid #ddd', borderRadius:8}}>
      <img src="/logo.png" alt="Langunana" style={{width:120, display:'block', margin:'auto'}}/>
      <h2 style={{textAlign:'center'}}>Langunana Community — Login</h2>
      <form onSubmit={handle}>
        <input required placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} style={{width:'100%',padding:8,margin:'8px 0'}}/>
        <input required type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} style={{width:'100%',padding:8,margin:'8px 0'}}/>
        <button style={{width:'100%',padding:10}}>Login</button>
      </form>
      <div style={{textAlign:'center', marginTop:10}}>
        <a href="/signup">Create account</a>
      </div>
    </div>
  )
}
