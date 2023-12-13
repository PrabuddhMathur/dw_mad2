<template>
    <div>
        <!-- <FlashErrorView /> -->
        <div class="container-fluid">
        <div class="row">        
            <div class="col-6 d-flex justify-content-start"></div>      
            <div class="col-5 d-flex justify-content-end">                
                <form @submit.prevent="register" style="margin-top: 50px;">
                    <h1 class="text-center mb-4" style="font-family: 'Bagel Fat One'; color: #D81159;">Welcome to Grocilla!</h1>
                    <h2 class="text-center">Sign Up!</h2>
                    <br>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="inlineRadio1" value="manager" v-model="role">
                        <label class="form-check-label" for="inlineRadio1">Store Manager</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="inlineRadio2" value="user" checked v-model="role">
                        <label class="form-check-label" for="inlineRadio2">User</label>
                    </div>

                    <br>
                    <div class = "form-group">
                        <label for="fname">First Name</label><br>
                        <input required id="fname" name="fname" class="form-control" type="text" placeholder="Enter your first name" v-model="fname">
                    </div>
                    <br>
                    <div class = "form-group">
                        <label for="lname">Last Name</label><br>
                        <input required id="lname" name="lname" class="form-control" type="text" placeholder="Enter your last name" v-model="lname">
                    </div>

                    <br>

                    <div class = "form-group">
                        <label for="username">Username</label><br>
                        <input required id="username" name="username" class="form-control" type="text" placeholder="Enter your username" v-model="username">
                    </div>
            
                    <br>
            
                    <div class = "form-group">
                        <label for="password1">Password</label><br>
                        <input required id="password1" class="form-control" type="password" placeholder="Enter your password" v-model="password">
                    </div>
            
                    <br>
                    <div class = "form-group">
                        <label for="password2"> Re-type Password</label><br>
                        <input required id="password2" class="form-control" type="password" placeholder="Retype the password" v-model="password2">
                    </div>
                    <br>
            
                    <div class="form-group text-center"><button type="submit" class="btn btn-dark">Register</button></div>
                    <br><br>Already a member? <a href="/login">Sign In!</a>
                    <!-- <br><br>Signing In as Manager?<a type="button" href="/admin_login">Admin Login</a> -->
                </form>            
            </div>
        </div>
        </div>
    </div>
    
</template>
<script>
import axios from 'axios';
import FlashErrorView from "./FlashErrorView.vue";

export default {
    components: {
        FlashErrorView
    },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            username: "",
            role: "user",
            password: "",
            password2:"",
            fname: "",
            lname: "",
			token:"",
			expiry:""
        }
    },
    methods: {
        async register() {
            if (this.password != this.password2) {
                alert("Passwords do not match!");
            }
            await axios
            .post("http://127.0.0.1:1430/api/register", {
                username: this.username,
                password: this.password,
                fname: this.fname,
                lname: this.lname,
                role: this.role
            })
            .then((response)=>response.data)
            .then((response) => {
                if ("Error" in response){
                        throw response
                    }
                    else{return response}
            })
            .then((response) => {
					this.token = response.token
					this.expiry = response.expiry
					this.userSession = {
					token: this.token,
					expiry: this.expiry,
					};
					localStorage.setItem("userSession", JSON.stringify(this.userSession));
					location.href="/login"
					
					})
					.catch((response)=>{
						alert(response['message'])
					})
        }
    }
}
</script>