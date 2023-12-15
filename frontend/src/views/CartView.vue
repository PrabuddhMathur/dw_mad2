<template>
<div>
    <Navbar />
    <div class="container mb-4">
    <div class="text-center my-4" >
        <h3>Your Cart</h3>
    </div>
    <!-- loop for products in specific category -->
    
    <div v-if="bookings.length > 0" class="container mb-4">
        <div v-for="booking in bookings" :key="booking.bookingid">
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-3">
                                    <b>{{ booking.product.pname }}</b>
                                </div>
                                <div class="col-2">
                                    {{ booking.quantity_of_item }} {{ booking.product.unit }}
                                </div>
                                <div class="col-2">
                                    Rs. {{ booking.quantity_of_item*booking.product.rateperunit }}
                                </div>
                                
                                <div v-if="bookings.product.quantity > 0">
                                <div class="col-2">
                                    <button class="btn btn-secondary btn-sm mx-auto d-grid col-12" type="button" data-bs-toggle="modal" data-bs-target="#{{ booking['bookingid'] }}AddToCartModal">Review</button>
                                </div>
                                <div class="col-2">
                                    <a href="/bookings/buy/{{ booking['bookingid'] }}" class="btn btn-dark btn-sm mx-auto d-grid col-12" type="submit">Buy</a>
                                </div>
                                <AddToCartModal />
                                </div>
                                
                                <!-- Modal -->
                                <!-- <div class="modal fade" id="{{ booking['bookingid'] }}AddToCartModal">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5">Review: {{ booking['product']['pname'] }}</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <form method = "POST", action = "/edit/bookings/{{ booking['bookingid'] }}">
                                                <div class="modal-body">
                                                    <div class="form-floating mb-3">
                                                        <input type="text" class="form-control" value='In Stock' id="Availability" readonly>
                                                        <label for="Availability">Availability</label>
                                                    </div>
                                                    <div class="form-floating mb-3">
                                                        <input type="number" class="form-control" id="Quantity{{ booking['bookingid'] }}" value="{{ booking['quantity_of_item'] }}" name="Quantity" min="1" max="{{ booking['product_id']['quantity'] }}" oninput="calculateTotal{{ booking['bookingid'] }}()">
                                                        <label for="Quantity{{ booking['bookingid'] }}">Quantity</label>
                                                    </div>
                                                    <div class="form-floating mb-3">
                                                        <input type="number" class="form-control" value="{{ booking['product']['rateperunit'] }}" id="Price{{ booking['bookingid'] }}" readonly>
                                                        <label for="Price{{ booking['bookingid'] }}">Price</label>
                                                    </div>
                                                    <div class="form-floating mb-3">
                                                        <input type="number" name="Total" class="form-control" value="" id="Total{{ booking['bookingid'] }}" readonly>
                                                        <label for="Total{{ booking['bookingid'] }}">Total</label>
                                                    </div>
                                                </div>
                                                <div class="modal-footer">
                                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                    <button type="submit" class="btn btn-primary">Done</button>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                                </div> -->
                                
                                <div v-else class="col-4">
                                <button class="btn btn-outline-dark btn-sm mx-auto d-grid col-12" type="button" disabled>Out Of Stock</button>
                                </div>
                                
                                <div class="col-1">
                                    <a href="/delete/booking/{{ booking['bookingid'] }}" class="btn btn-danger btn-md mx-auto d-grid col-12" type="submit"><i class="fa-solid fa-trash-can"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- <script>
                        function calculateTotal{{ booking['bookingid'] }}(){
                            var quantity = document.getElementById("Quantity{{ booking['bookingid'] }}").value;
                            var price = document.getElementById("Price{{ booking['bookingid'] }}").value;
                            var totalPrice = quantity*price;
                            return document.getElementById("Total{{ booking['bookingid'] }}").value = totalPrice;
                        }
                    </script> -->
                </div>
            </div>
        </div>
    </div>

    
    <div v-else class="container mb-4">
    <h6>Your cart seems to be empty at the moment.</h6>
    </div>
          
    </div> 
    <br><br><br>
    <footer class="py-3 bg-dark bg-gradient text-white fixed-bottom">
        <div class="container">
            <div class="row">
                <div class="d-flex col-6 justify-content-start">
                    Grand Total : {{ total }}
                </div>
                <div class="d-flex col-6 justify-content-end">
                    <a href="/bookings/buy_all" class="btn btn-outline-light btn-sm mx-2" type="submit">Buy All</a>
                </div>
            </div>
        </div>
    </footer>
    </div>

</template>

<script>
import Navbar from '../components/user/Navbar.vue';
import AddToCartModal from '../components/user/modals/AddToCartModal.vue';
import axios from "axios";


export default {
    components: {
        Navbar,
        AddToCartModal
        },
    data() {
        return {
            bookings: []
        }
    },
    methods: {
        async fetchBookings() {
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
        },
        async deleteCategory(cid){
            await axios
            .delete("http://127.0.0.1:1430/admin-api/category/"+cid)
            .then((response)=>response)
            .then((response)=>response.data)
            .then((results)=>{
                this.categories = this.categories.filter(category => category.cid !== cid);
                console.log(results)
                })
        },
    },
    computed:{
        getCategories(){return this.categories;}
    },
    async beforeMount() {
        await this.fetchCategories();
    },
    mounted() {
		document.title = "Admin Dashboard";
	}
}
</script>
