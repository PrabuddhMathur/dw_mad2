<template>
    <div>
        <Navbar />
        <div class="text-center my-4" >
            <button class="btn btn-dark" style="margin-left: 5px" data-bs-toggle="modal" data-bs-target="#SearchCategoryModal">Search Category</button>
            <!-- Search Category Modal -->
            <SearchCategoryModal />
            <button class="btn btn-dark" style="margin-left: 5px" data-bs-toggle="modal" data-bs-target="#SearchProductModal">Search Product</button>
            <!-- Search Product Modal -->
            <SearchProductModal />
        </div>
        <!-- {% for category in categories %} -->
        <div class="container mb-4">
            <div class="row">
                <h5 class="col-3" style="margin-top: 6px; font-family: 'Bangers';font-size: 28px;">{{ category["cname"] }}</h5>
            </div>
            <hr>
            <!-- {% if category['products']|length > 0 %} -->
            <div class="row row-cols-2 row-cols-md-3 row-cols-lg-5  g-4">
                <!-- loop for products in specific category -->
                <!-- {% for product in category['products'] %}             -->
                <div class="col">
                    <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">{{ product['pname'] }}</h5>
                        Quantity: {{ product['quantity'] }} <br>
                        Rate: Rs. {{ product['rateperunit'] }}/{{ product['unit'] }}
                    </div>
                    <div class="card-footer d-flex justify-content-center">
                        <!-- {% if product['quantity']>0 %}                     -->
                        <button class="btn btn-outline-dark btn-sm mx-2" type="button" data-bs-toggle="modal" data-bs-target="#{{ product['pid'] }}AddToCartModal"><i class="fa-solid fa-cart-plus"></i></button>
                        <!-- AddToCartModal -->
                        <AddToCartModal :product="product" />
                        <!-- {% else %} -->
                        <button class="btn btn-outline-dark btn-sm mx-2 " type="button" disabled>Out Of Stock</button>
                        <!-- {% endif %} -->
                    </div>                
                    </div>
                </div>           
                <!-- {% endfor %} -->
            </div>
            <!-- {% else %} -->
            <h6>No items here yet.</h6>
            <!-- {% endif %} -->
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
            categories: []
        }
    },
    methods: {
        async fetchCategories() {
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
        }
    },
    computed:{
        getCategories(){return this.categories;}
    },
    async beforeMount() {
        await this.fetchCategories();
    },
    mounted() {
		document.title = "User Dashboard";
	}
}
</script>
