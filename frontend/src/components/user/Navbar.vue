<template>
    <nav class="navbar navbar-expand-lg bg-dark sticky-top bg-gradient">
        <div class="container">
            <a class="navbar-brand" href="/" style="font-family: 'Bagel Fat One';font-size: 32px; color: aliceblue;">Grocilla</a>
            <span class="navbar-text" style="font-size: 28px; color: aliceblue;">Welcome user {{ username }}!</span>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <div class="navbar-nav ms-auto mb-2 mb-lg-0 gap-2">
                    <a href="/cart" class="btn btn-outline-light" style="margin-left: 5px">My Cart</a>
                    <a href="/orders" class="btn btn-outline-light" style="margin-left: 5px">My Orders</a>
                    <a href="/logout" class="btn btn-outline-light" style="margin-left: 5px">Logout</a>
                </div>
            </div>
        </div>
    </nav>
</template>
<script>
import axios from "axios";
export default{
    data(){
        return{
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            username: "",   
        }
    },
    methods:{
        async getUsername(){
            if (this.userSession){
                axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .get("http://127.0.0.1:1430/api/username")
                .then((response) => response)
                .then((response) => response.data)
                .then((results) => {
                    this.username = results['username'];
                })
            }else{alert("Please login and try again!")}
        }
    },
    async beforeMount() {
        await this.getUsername();
    },
}
</script>