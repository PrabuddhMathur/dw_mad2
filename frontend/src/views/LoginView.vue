<template>
    <div>
        <!-- <FlashErrorView /> -->
        <div class="container-fluid">
        <div class="row">  
            <div class="col-6 d-flex justify-content-start"></div>      
            <div class="col-5 d-flex justify-content-end">
                <form @submit.prevent="login"  style="margin-top: 150px;">
                    <h1 class="text-center mb-4" style="font-family: 'Bagel Fat One'; color: #D81159;">Welcome to Grocilla!</h1>
                    <h2 class="text-center">Login</h2>
                    <div class = "form-group">
                        <label for="username">Username</label><br>
                        <input required id="username" class="form-control" type="text" placeholder="Enter your username" v-model="username">
                    </div>
            
                    <br>
            
                    <div class = "form-group">
                        <label for="password">Password</label><br>
                        <input required id="password" class="form-control" type="password" placeholder="Enter your password" v-model="password">
                    </div>
            
                    <br>
            
                    <div class="form-group text-center"><button type="submit" class="btn btn-dark">Login</button></div>
                    <br><br>Haven't registered yet? <a href="/register">Sign Up!</a>
                </form>            
            </div>
        </div>
        </div>
    </div>
</template>
<script>
import FlashErrorView from "../components/FlashStatusView.vue";
import axios from "axios";
export default {
    components: {
        FlashErrorView
    },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            username: "",
            password: ""
        };
    },
	methods:{
		async login(){
			await axios
				.post("http://127.0.0.1:1430/api/login",{
					username:this.username,
					password:this.password
				})
				.then((response)=>response)
				.then((response)=>response.data)
				.then((response)=>{
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
				location.href="/dashboard"
				
				})
				.catch((response)=>{
					alert(response['message'])
				})
				
				
		}
	}
}

</script>

<!-- <style scoped>

        body {
            background-image: url("../static/grocillabg.avif");
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
            background-color: #464646;
            /* opacity: 1;
            transition: opacity 1s; */
            }
</style> -->