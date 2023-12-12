<template>
    <div>
        <FlashErrorView />
        <div class="container-fluid">
        <div class="row">  
            <div class="col-6 d-flex justify-content-start"></div>      
            <div class="col-5 d-flex justify-content-end">
                <form method="POST" action="/user_login" style="margin-top: 150px;">
                    <h1 class="text-center mb-4" style="font-family: 'Bagel Fat One'; color: #D81159;">Welcome to Grocilla!</h1>
                    <h2 class="text-center">Login</h2>
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
            
                    <div class="form-group text-center"><button type="submit" class="btn btn-dark">Login</button></div>
                    <br><br>Haven't registered yet? <a href="/register">Sign Up!</a>
                    <br><br>Signing In as Manager?<a type="button" href="/admin_login">Admin Login</a>
                </form>            
            </div>
        </div>
        </div>
    </div>
</template>
<script>
import FlashErrorView from "./FlashErrorView.vue";

export default {
    components: {
        FlashErrorView
    }
}

</script>

<style>

        body {
            background-image: url("../static/grocillabg.avif");
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
            background-color: #464646;
            opacity: 0;
            transition: opacity 1000000s;
            }
</style>