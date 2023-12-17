<template>
    <div>
        <Navbar />
        <div class="text-center my-4" >
            <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#AddCategoryModal"><i class="fa fa-plus"></i> Add Category</button>
        </div>
        <AddCategoryModal />
        <template v-if="categories.length > 0">
            <div v-for="category in categories" :key="category.cid">
                <div class="container mb-4">
                    <div  class="row">
                        <h5 class="col-3" style="margin-top: 6px; font-family: 'Bangers';font-size: 28px;">{{ category.cname }}</h5>
                        <div class="d-flex col-2 align-items-center">
                            <button class="btn btn-dark mx-2" type="button" data-bs-toggle="modal" :data-bs-target="'#'+ category.cid + 'EditCategoryModal'"><i class="fa-solid fa-pen"></i></button>
                            <EditCategoryModal :category="category" />
                            <a @click="deleteCategory(category.cid)" class="btn btn-danger" type="submit"><i class="fa-solid fa-trash-can"></i></a>
                        </div>
                    </div>
                    <hr>
                    <div   v-if="category.products.length>0" class="row row-cols-2 row-cols-md-3 row-cols-lg-5  g-4">
                        <div v-for="product in category.products" :key="product" class="col">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">{{ product.pname }}</h5>
                                    Quantity: {{ product.quantity }}<br>
                                    Rate: Rs. {{ product.rateperunit }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <h6 v-else >No items here yet. Click on Add Product to add items!</h6>
                </div>
            </div>
        </template>
        <div v-else class="container mb-4">
            <h6>No categories created yet. Click on Add Category to create one!</h6>
        </div>

    </div>
    
</template>

<script>
import Navbar from './Navbar.vue';
import AddCategoryModal from './modals/AddCategoryModal.vue';
import EditCategoryModal from './modals/EditCategoryModal.vue';
import axios from "axios";


export default {
    components: {
        Navbar,
        AddCategoryModal,
        EditCategoryModal
    },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            categories: []
        }
    },
    methods: {
        async fetchCategories() {
            if (this.userSession){
                axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .get("http://127.0.0.1:1430/api/categories")
                    .then((response) => response)
                    .then((response) => response.data)
                    .then((results) => {
                        this.categories = results;
                    })
                    .catch(()=>{
                        console.error("Category error: ", error)
                    });
            }else{alert("Please login and try again!")}
        },
        async deleteCategory(cid){
            if (this.userSession){
                axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .delete("http://127.0.0.1:1430/admin-api/category/"+cid)
                .then((response)=>response)
                .then((response)=>response.data)
                .then((results)=>{
                    this.categories = this.categories.filter(category => category.cid !== cid);
                    console.log(results)
                    })
            }else{alert("Please login and try again!")}
        },
    },
    async beforeMount() {
        await this.fetchCategories();
    },
    mounted() {
		document.title = "Admin Dashboard";
	}
}
</script>
