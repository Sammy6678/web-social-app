import React, {useState} from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_BASE || 'https://<BACKEND_HOST>'

export default function Signup(){
  const [form,setForm] = useState({username:'',email:'',password:'',gender:'Male'})

  async function handle(e){
    e.preventDefault()
    try{
      const fd = new FormData()
      fd.append('username', form.username)
      fd.append('email', form.email)
      fd.append('password', form.password)
      fd.append('gender', form.gender)
      const res = await axios.post(`${API}/signup`, fd)
      alert('Signup successful! Please login.')
      window.location.href = '/'
    }catch(err){
      alert(err?.response?.data?.detail || 'Signup failed')
    }
  }

  return (
    <div style={{maxWidth:420, margin:'40px auto', padding:20, border:'1px solid #ddd', borderRadius:8}}>
      <h2 style={{textAlign:'center'}}>Langunana — Signup</h2>
      <form onSubmit={handle}>
        <input required placeholder="Username" value={form.username} onChange={e=>setForm({...form,username:e.target.value})} style={{width:'100%',padding:8,margin:'8px 0'}}/>
        <input required type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} style={{width:'100%',padding:8,margin:'8px 0'}}/>
        <input required type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} style={{width:'100%',padding:8,margin:'8px 0'}}/>
        <select value={form.gender} onChange={e=>setForm({...form,gender:e.target.value})} style={{width:'100%',padding:8,margin:'8px 0'}}>
          <option>Male</option><option>Female</option>
        </select>
        <button style={{width:'100%',padding:10}}>Signup</button>
      </form>
    </div>
  )
}
