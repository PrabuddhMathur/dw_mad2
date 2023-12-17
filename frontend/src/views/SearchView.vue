<template>
    <div>
        <Navbar />
        <template v-if="search_by=='category'">
            <br>
            <h3 class="text-center" >Showing results for category : {{ query }}</h3>
            <template v-if="categories.length>0">
                <div v-for="category in categories" :key="category.cid">
                    <div class="container mb-4">
                        <div class="row">
                            <h5 class="col-3" style="margin-top: 6px; font-family: 'Bangers';font-size: 28px;">{{ category.cname }}</h5>
                        </div>
                        <hr>
                        <div v-if="category.products.length>0" class="row row-cols-2 row-cols-md-3 row-cols-lg-5  g-4">
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
                                    <AddToCartModal :category_name=category.cname :product="product" />
                                </div>                
                                </div> 
                            </div>           
                        </div>
                        <h6 v-else>No items here yet.</h6>
                    </div>
                </div>
            </template>
            <h6 v-else>No Categories found!</h6>
        </template>
        <template v-else>
            <br>
            <h3 class="text-center">Showing results for product : {{ query }}</h3>
            <div class="container mb-4">
                <div v-if="products.length>0" class="row row-cols-2 row-cols-md-3 row-cols-lg-5  g-4">
                    <div v-for="product in products" :key="product.pid" class="col">
                        <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">{{ product.pname }}</h5>
                            Quantity: {{ product.quantity }} <br>
                            Rate: Rs. {{ product.rateperunit }}/{{ product.unit }}
                        </div>
                        <div class="card-footer d-flex justify-content-center">
                            <button v-if="product.quantity>0" class="btn btn-outline-dark btn-sm mx-2" type="button" data-bs-toggle="modal" :data-bs-target="'#'+product.pid+'AddToCartModal'"><i class="fa-solid fa-cart-plus"></i></button>
                            <button v-else class="btn btn-outline-dark btn-sm mx-2 " type="button" disabled>Out Of Stock</button>
                            <AddToCartModal :category_name=product.cname :product="product" />
                        </div>                
                        </div> 
                    </div>           
                </div>
                <h6 v-else>No items here yet.</h6>
            </div>
        </template>
    </div>
</template>
<script>
import axios from 'axios';
import Navbar from '../components/user/Navbar.vue';
import AddToCartModal from '../components/user/modals/AddToCartModal.vue'
export default {
    components: {
        Navbar,
        AddToCartModal
    },
    props: {
        search_by: {
        type: String,
        default: '' // Default value if 'search_by' is not provided in the URL
        },
        query: {
        type: String,
        default: '' // Default value if 'query' is not provided in the URL
        }
    },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            categories: [],
            products: []
        }
    },
    methods: {
        async searchCategories(){
                if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                    await axios
                    .post("http://127.0.0.1:1430/user-api/search/category",{
                        category:this.query
                    })
                    .then((response)=>response.data)
                    .then((response)=>{this.categories=response})
                    // this.$router.push({name:"search",query:{search_by:'category',q:this.category}})
                }else{
                    alert("Please login and try again!")
                }
        },
        async searchProducts(){
                if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                    await axios
                    .post("http://127.0.0.1:1430/user-api/search/product",{
                        product:this.query
                    })
                    .then((response)=>response.data)
                    .then((response)=>{this.products=response})
                    // this.$router.push({name:"search",query:{search_by:'category',q:this.category}})
                }else{
                    alert("Please login and try again!")
                }
        },
    },
    async beforeMount() {
        await this.searchCategories();
        await this.searchProducts();
    },
    mounted() {
		document.title = "Search results for "+this.query;
	}
}
</script>
