import React, {useState} from 'react'
import {useHistory} from 'react-router-dom'
import styled from "styled-components";
import { useFormik } from "formik"
import * as yup from "yup"


function Authentication({updateUser}) {
  const [signUp, setSignUp] = useState(false)
  const [errors, setErrors] = useState(null)
  
  const history = useHistory()

  const handleClick = () => setSignUp((signUp) => !signUp)
  const formSchema = yup.object().shape({
    name: yup.string().required("Please enter a user name"),
    password: yup.string().required("Please enter a password"),
    email: yup.string().email()
  })

  const formik = useFormik({
    initialValues: {
      name:'',
      email:'',
      password:''
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
        setErrors(null)
        fetch(signUp ? '/signup':'/login',{
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        })
        .then(res => {
          if(res.ok){
            res.json().then(user => {
              console.log(user)
              updateUser(user)
              history.push('/')
            })
          } else {
            //12✅ Handle user errors if Auth fails
              //12.1 add errors to state
              //12.2 conditionally render the errors in jsx
            res.json().then(error => {
              console.error(error)
              setErrors(error)
            })
          }
        })
       
    },
  })

    return (
        <> 
        {errors && <h3 style={{color: 'red'}}>{errors.message}</h3>}
        <h2>Please Log in or Sign up!</h2>
        <h2>{signUp?'Already a member?':'Not a member?'}</h2>
        <button onClick={handleClick}>{signUp?'Log In!':'Register now!'}</button>
        <Form onSubmit={formik.handleSubmit}>
          {/* {formik.errors && Object.values(formik.errors).map(e => <div>{e}</div>)}
          {formik.touched && Object.entries(formik.touched).map(([k, v]) => <div>{`the field ${k} was touched: ${v}`}</div>)} */}
        <label>
          Username
          </label>
        <input type='text' name='name' value={formik.values.name} onChange={formik.handleChange} onBlur={formik.handleBlur}/>
        {formik.touched.name && formik.errors.name && <div style={{color: 'red'}}>{formik.errors.name}</div>}
        <label>
           Password
           </label>
           <input type='password' name='password' value={formik.values.password} onChange={formik.handleChange} onBlur={formik.handleBlur}/>
           {formik.touched.password && formik.errors.password && <div style={{color: 'red'}}>{formik.errors.password}</div>}
        {signUp&&(
          <>
          <label>
          Email
          </label>
          <input type='text' name='email' value={formik.values.email} onChange={formik.handleChange} onBlur={formik.handleBlur}/>
          {formik.touched.email && formik.errors.email && <div style={{color: 'red'}}>{formik.errors.email}</div>}
           
           </>
        )}
        <input type='submit' value={signUp?'Sign Up!':'Log In!'} />
      </Form>
        </>
    )
}

export default Authentication

export const Form = styled.form`
display:flex;
flex-direction:column;
width: 400px;
margin:auto;
font-family:Arial;
font-size:30px;
input[type=submit]{
  background-color:#42ddf5;
  color: white;
  height:40px;
  font-family:Arial;
  font-size:30px;
  margin-top:10px;
  margin-bottom:10px;
}
`