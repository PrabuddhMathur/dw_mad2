<template>
    <div>
        <Navbar />
        <div class="text-center my-4" >
            <h3>Store Manager Requests</h3>
        </div>
        <div class="container mb-4">               
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="row" >
                                <div class="col-2 text-center">
                                    <h5>Name</h5>
                                </div>
                                <div class="col-8 text-center">
                                    <h5>Username</h5>
                                </div>
                                <div class="col-2 text-center">
                                    <h5>Action</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>               
        </div>
        <div v-if="users.length > 0" class="container mb-4">
                <div v-for="user in users" :key="user.id">
                    <div class="row">
                        <div class="col">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-2 text-center">
                                            {{ user.fname }} {{ user.lname }}
                                        </div>
                                        <div class="col-8 text-center">
                                            {{ user.username }}
                                        </div>
                                        <div class="col-1 text-center">
                                            <a @click="approveUser(user.id)" class="btn btn-success btn-md mx-auto d-grid col-12" type="submit">Approve</a>
                                        </div>
                                        <div class="col-1 text-center">
                                            <a @click="deleteUser(user.id)" class="btn btn-danger btn-md mx-auto d-grid col-12" type="submit">Reject</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </div>
        <div v-else class="container mb-4">
            <h6>No manager approval requests currently.</h6>
        </div>

        <div class="text-center my-4" >
            <h3>Category Management Requests</h3>
        </div>
        <div class="container mb-4">
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-2 text-center">
                                    <h5>Category Name</h5>
                                </div>
                                <div class="col-8 text-center">
                                    <h5>Request</h5>
                                </div>
                                <div class="col-2 text-center">
                                    <h5>Action</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="categories.length > 0" class="container mb-4">
                <div v-for="category in categories" :key="category.id">
                    <div class="row">
                        <div class="col">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-2 text-center">
                                            {{ category.cname }}
                                        </div>
                                        <div v-if="category.request_type=='Update'" class="col-8 text-center">
                                            {{ category.request_type }} category : {{ category.updated_cname }}
                                        </div>
                                        <div v-else class="col-8 text-center">
                                            {{ category.request_type }} category
                                        </div>
                                        <div class="col-1 text-center">
                                            <a @click="approveCategory(category.id)" class="btn btn-success btn-md mx-auto d-grid col-12" type="submit">Approve</a>
                                        </div>
                                        <div class="col-1 text-center">
                                            <a @click="deleteCategory(category.id)" class="btn btn-danger btn-md mx-auto d-grid col-12" type="submit">Reject</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </div>
        <div v-else class="container mb-4">
            <h6>No requests currently.</h6>
        </div>
    </div>

</template>
<script>
import Navbar from './Navbar.vue';
import axios from "axios";

export default {
    components: {
        Navbar,
    },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            categories: [],
            users: []
        }
    },
    methods: {
        async fetchCategories() {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
            .get("http://127.0.0.1:1430/admin-api/approval/categories")
                .then((response) => response)
                .then((response) => response.data)
                .then((results) => {
                    this.categories = results;
                })
                .catch((error)=>{
                    console.error("Category fetch error: ", error)
                });
            }else{alert("Please login and try again!")}
        },
        async fetchUsers() {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
            .get("http://127.0.0.1:1430/admin-api/approval/users")
                .then((response) => response)
                .then((response) => response.data)
                .then((results) => {
                    this.users = results;
                })
                .catch((error)=>{
                    console.error("User fetch error: ", error)
                });
            }else{alert("Please login and try again!")}
        },
        async approveUser(user_id){
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
            .get("http://127.0.0.1:1430/admin-api/approval/user/"+user_id)
                .then((response)=>response)
                .then((response)=>response.data)
                .then((results)=>{
                    this.users = this.users.filter(user => user.id !== user_id);
                    console.log(results)
                })
        }else{alert("Please login and try again!")}
        },
        async deleteUser(user_id){
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
            .delete("http://127.0.0.1:1430/admin-api/approval/user/"+user_id)
                .then((response)=>response)
                .then((response)=>response.data)
                .then((results)=>{
                    this.users = this.users.filter(user => user.id !== user_id);
                    console.log(results)
                    })
        }else{alert("Please login and try again!")}
        },
        async approveCategory(approval_id){
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
            .get("http://127.0.0.1:1430/admin-api/approval/category/"+approval_id)
                .then((response)=>response)
                .then((response)=>response.data)
                .then((results)=>{
                    this.categories = this.categories.filter(category => category.id !== approval_id);
                    console.log(results)
                    })
        }else{alert("Please login and try again!")}
        },
        async deleteCategory(approval_id){
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
            .delete("http://127.0.0.1:1430/admin-api/approval/category/"+approval_id)
                .then((response)=>response)
                .then((response)=>response.data)
                .then((results)=>{
                        this.categories = this.categories.filter(category => category.id !== approval_id);
                        console.log(results)
                })
                }else{alert("Please login and try again!")}
        }
    },
    async beforeMount() {
        await this.fetchCategories();
        await this.fetchUsers();
    },
    mounted() {
		document.title = "Admin Approvals";
	}
}
</script>