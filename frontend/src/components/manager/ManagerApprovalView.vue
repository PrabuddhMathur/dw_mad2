<template>
    <div>
        <Navbar />
        <div class="text-center my-4" >
            <h3>Pending Category Management Requests</h3>
        </div>
        <div class="container mb-4">
                    <div class="row">
                        <div class="col">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-4 text-center">
                                            <h5>Category Name</h5>
                                        </div>
                                        <div class="col-8 text-center">
                                            <h5>Request</h5>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
        </div>
        <!-- loop for products in specific category -->
        <div v-if="categories.length > 0" class="container mb-4">
                <div v-for="category in categories" :key="category.id">
                    <div class="row">
                        <div class="col">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-4 text-center">
                                            {{ category.cname }}
                                        </div>
                                        <div v-if="category.request_type=='Update'" class="col-8 text-center">
                                            {{ category.request_type }} category : {{ category.updated_cname }}
                                        </div>
                                        <div v-else class="col-8 text-center">
                                            {{ category.request_type }} category
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
        }
    },
    methods: {
        async fetchCategories() {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
            .get("http://127.0.0.1:1430/manager-api/approval/categories")
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
    },
    async beforeMount() {
        await this.fetchCategories();
    },
    mounted() {
		document.title = "Pending Approvals";
	}
}
</script>
