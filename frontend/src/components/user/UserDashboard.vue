<template>
    <div>
        <Navbar />
        <div class="text-center my-4" >
            <button class="btn btn-dark" style="margin-left: 5px" data-bs-toggle="modal" data-bs-target="#SearchCategoryModal">Search Category</button>
            <!-- Search Category Modal -->
            <SearchCategoryModal :categories=categories />
            <button class="btn btn-dark" style="margin-left: 5px" data-bs-toggle="modal" data-bs-target="#SearchProductModal">Search Product</button>
            <!-- Search Product Modal -->
            <SearchProductModal :products=products />
        </div>
        <!-- {% for category in categories %} -->
        <div v-for="category in categories" :key="category.cid">

            <div class="container mb-4">
                <div class="row">
                    <h5 class="col-3" style="margin-top: 6px; font-family: 'Bangers';font-size: 28px;">{{ category.cname }}</h5>
                </div>
                <hr>
                <!-- {% if category['products']|length > 0 %} -->
                <div v-if="category.products.length>0" class="row row-cols-2 row-cols-md-3 row-cols-lg-5  g-4">
                    <!-- loop for products in specific category -->
                    <!-- {% for product in category['products'] %}             -->
                    <div v-for="product in category.products" :key="product.pid" class="col">
                        <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">{{ product.pname }}</h5>
                            Quantity: {{ product.quantity }} <br>
                            Rate: Rs. {{ product.rateperunit }}/{{ product.unit }}
                        </div>
                        <div class="card-footer d-flex justify-content-center">
                            <button v-if="product.quantity>0" class="btn btn-outline-dark btn-sm mx-2" type="button" data-bs-toggle="modal" :data-bs-target="'#'+product.pid+'AddToCartModal'"><i class="fa-solid fa-cart-plus"></i></button>
                            <button v-else class="btn btn-outline-dark btn-sm mx-2 " type="button" disabled>Out Of Stock</button>
                            <!-- AddToCartModal -->
                            <AddToCartModal :category_name=category.cname :product="product" />

                        </div>                
                        </div> 
                    </div>           
                    <!-- {% endfor %} -->
                </div>
                <!-- {% else %} -->
                <h6 v-else>No items here yet.</h6>
                <!-- {% endif %} -->
            </div>

        </div>

    </div>
</template>
<script>
import Navbar from './Navbar.vue';
import AddToCartModal from './modals/AddToCartModal.vue';
import SearchCategoryModal from './modals/SearchCategoryModal.vue';
import SearchProductModal from './modals/SearchProductModal.vue';
import axios from "axios";

export default {
    components: {
        Navbar,
        AddToCartModal,
        SearchCategoryModal,
        SearchProductModal
    },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            categories: [],
            products: []
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
        async fetchProducts() {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .get("http://127.0.0.1:1430/api/products")
                    .then((response) => response)
                    .then((response) => response.data)
                    .then((results) => {
                        this.products = results;
                    })
                    .catch(()=>{
                        console.error("Product error: ", error)
                    });
            }else{alert("Please login and try again!")}
        }
    },
    async beforeMount() {
        await this.fetchCategories();
        await this.fetchProducts();
    },
    mounted() {
		document.title = "User Dashboard";
	}
}
</script>
