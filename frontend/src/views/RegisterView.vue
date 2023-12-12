<template>
    <div>
        <FlashErrorView />
        <div class="container-fluid">
        <div class="row">        
            <div class="col-6 d-flex justify-content-start"></div>      
            <div class="col-5 d-flex justify-content-end">                
                <form method="POST" action="/register" style="margin-top: 50px;">
                    <h1 class="text-center mb-4" style="font-family: 'Bagel Fat One'; color: #D81159;">Welcome to Grocilla!</h1>
                    <h2 class="text-center">Sign Up!</h2>
                    <div class = "form-group">
                        <label for="fname">First Name</label><br>
                        <input required id="fname" name="fname" class="form-control" type="text" placeholder="Enter your first name">
                    </div>

                    <br>

                    <div class = "form-group">
                        <label for="lname">Last Name</label><br>
                        <input required id="lname" name="lname" class="form-control" type="text" placeholder="Enter your last name">
                    </div>

                    <br>

                    <div class = "form-group">
                        <label for="username">Username</label><br>
                        <input required id="username" name="username" class="form-control" type="text" placeholder="Enter your username">
                    </div>
            
                    <br>
            
                    <div class = "form-group">
                        <label for="password">Password</label><br>
                        <input required id="password" name="password" class="form-control" type="password" placeholder="Enter your password">
                    </div>
            
                    <br>
            
                    <div class="form-group text-center"><button type="submit" class="btn btn-dark">Register</button></div>
                    <br><br>Already a member? <a href="/user_login">Sign In!</a>
                    <br><br>Signing In as Manager?<a type="button" href="/admin_login">Admin Login</a>
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
            password: "",
            password2:"",
            fname: "",
            lname: "",
			token:"",
			expiry:""
        }
    },
    methods: {
        register() {
            if (this.password != this.password2) {
                alert("Passwords do not match!");
                return;
            }
            axios.post("/register", {
                username: this.username,
                password: this.password,
                fname: this.fname,
                lname: this.lname
            }).then(response => {
                if (response.data.success) {
                    alert("Registration successful!");
                    this.username = "";
                    this.password = "";
                    this.password2 = "";
                    this.fname = "";
                    this.lname = "";
                    this.$router.push("/user_login");
                } else {
                    alert("Registration failed!");
                }
            }).catch(error => {
                alert("Registration failed!");
            });
        }
    }
}

</script>

<style scoped>

        body {
            background-image: url("../static/grocillabg.avif");
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
            background-color: #464646;
            opacity: 0;
            transition: opacity 1s;
            }
</style>