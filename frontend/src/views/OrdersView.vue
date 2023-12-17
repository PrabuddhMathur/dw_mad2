<template>
    <div>
    <Navbar />
    <div class="container mb-4">
    <div class="text-center my-4" >
        <h3>Your Orders</h3>
    </div>
    <!-- loop for products in specific category -->
    
    <div v-if="orders.length > 0">
        <div v-for="order in orders" :key="order.orderid">
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-3 text-center">
                                    <b>{{ order.product_name }}</b>
                                </div>
                                <div class="col-6 text-center">
                                    {{ order.quantity_of_product }} {{ order.product_unit }}
                                </div>
                                <div class="col-3 text-center">
                                    Rs. {{ order.totalprice }}
                                </div>
                                
                                
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    
    <div v-else class="container mb-4">
    <h6>No orders to show.</h6>
    </div>

    </div>
    </div>

</template>

<script>
import Navbar from '../components/user/Navbar.vue';
import axios from "axios";


export default {
    components: {
        Navbar
        },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            orders: []
        }
    },
    methods: {
        async fetchOrders() {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .get("http://127.0.0.1:1430/user-api/orders")
                    .then((response) => response)
                    .then((response) => response.data)
                    .then((results) => {
                        this.orders = results;
                    })
                    .catch(()=>{
                        console.error("Orders fetch error: ", error)
                    });
            }else{
                    alert("Please login and try again!")
                }
        },
        
    },
    async beforeMount(){
        await this.fetchOrders();
    },
    mounted(){
        document.title="Orders"
    }
}
</script>