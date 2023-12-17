<template>
<div>
    <Navbar />
    <div class="container mb-4">
    <div class="text-center my-4" >
        <h3>Your Cart</h3>
    </div>
    
    <div v-if="bookings.length > 0">
        <div v-for="booking in bookings" :key="booking.bookingid">
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-3 text-center">
                                    <b>{{ booking.product.pname }}</b>
                                </div>
                                <div class="col-2 text-center">
                                    {{ booking.quantity_of_item }} {{ booking.product.unit }}
                                </div>
                                <div class="col-2 text-center">
                                    Rs. {{ Number(booking.quantity_of_item)*Number(booking.product.rateperunit) }}
                                </div>
                                
                                <template v-if="booking.product.quantity > 0">
                                    <div class="col-2">
                                        <button class="btn btn-secondary btn-sm mx-auto d-grid col-12" type="button" data-bs-toggle="modal" :data-bs-target="'#'+ booking.bookingid +'ReviewCartModal'">Review</button>
                                    </div>
                                    <div class="col-2">
                                        <a @click="buyBooking(booking.bookingid);getTotal()" class="btn btn-dark btn-sm mx-auto d-grid col-12">Buy</a>
                                    </div>
                                    <ReviewCartModal :booking="booking" />
                                </template>
                                <div v-else class="col-4">
                                    <button class="btn btn-outline-dark btn-sm mx-auto d-grid col-12" type="button" disabled>Out Of Stock</button>
                                </div>
                                
                                <div class="col-1">
                                    <a @click="deleteBooking(booking.bookingid);getTotal()" class="btn btn-danger btn-md mx-auto d-grid col-12"><i class="fa-solid fa-trash-can"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
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
                        Grand Total : {{ this.gtotal }}
                    </div>
                    <div class="d-flex col-6 justify-content-end">
                        <a @click="buyAll()" class="btn btn-outline-light btn-sm mx-2" type="submit">Buy All</a>
                    </div>
                </div>
            </div>
        </footer>
    </div>
</template>

<script>
import Navbar from '../components/user/Navbar.vue';
import ReviewCartModal from '../components/user/modals/ReviewCartModal.vue';
import axios from "axios";

export default {
    components: {
        Navbar,
        ReviewCartModal
        },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            bookings: [],
            gtotal:0
        }
    },
    methods: {
        async fetchBookings() {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .get("http://127.0.0.1:1430/user-api/bookings")
                    .then((response) => response)
                    .then((response) => response.data)
                    .then((results) => {
                        this.bookings = results;
                    })
                    .catch(()=>{
                        console.error("Booking fetch error: ", error)
                    });
            }else{
                    alert("Please login and try again!")
                }
        },
        async buyBooking(bookingid) {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .get("http://127.0.0.1:1430/user-api/bookings/"+bookingid)
                    .then((response) => response)
                    .then((response) => response.data)
                    .then((results) => {
                        console.log(results);
                        this.bookings = this.bookings.filter(booking => booking.bookingid !== bookingid);
                        this.$router.push("/orders")
                    })
            }else{alert("Please login and try again!")}
        },
        async deleteBooking(bookingid) {
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .delete("http://127.0.0.1:1430/user-api/bookings/"+bookingid)
                    .then((response) => response)
                    .then((response) => response.data)
                    .then((results) => {
                        console.log(results);
                        this.bookings = this.bookings.filter(booking => booking.bookingid !== bookingid);
                        this.getTotal()
                    })
            }else{alert("Please login and try again!")}
        },
        getTotal(){
            this.gtotal=0
            for (const booking of this.bookings){
                if (booking.product.quantity>0)
                    this.gtotal+= booking.quantity_of_item*booking.product.rateperunit
                
            }
        },
        async buyAll(){
            if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .get("http://127.0.0.1:1430/user-api/bookings/buyall")
                    .then((response) => response)
                    .then((response) => response.data)
                    .then((results) => {console.log(results);this.$router.push("/orders")})
            }else{alert("Please login and try again!")}
        }
    },
    async beforeMount(){
        await this.fetchBookings();
        this.getTotal(); 
    },
    mounted(){
        document.title="User Cart"
    },
}
</script>
