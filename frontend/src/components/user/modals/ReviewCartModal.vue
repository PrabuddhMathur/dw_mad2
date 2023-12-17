<template>
    <div class="modal fade" :id="this.booking.bookingid +'ReviewCartModal'">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add To Cart: {{ this.booking.item_name }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="submitForm">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input type="text" class="form-control" value='In Stock' id="Availability" readonly>
                            <label for="Availability">Availability</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input v-model="quantity" type="number" class="form-control" :id="'Quantity'+ this.booking.bookingid" name="Quantity" min="1" :max="this.booking.product_id.quantity">
                            <label :for="'Quantity'+ this.booking.bookingid">Quantity</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input type="number" class="form-control" :value="this.booking.rateperunit" :id="'Price'+this.booking.bookingid" readonly>
                            <label :for="'Price'+this.booking.bookingid">Price</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input type="number" name="Total" class="form-control" :value="quantity*this.booking.rateperunit" :id="'Total'+this.booking.bookingid" readonly>
                            <label :for="'Total'+this.booking.bookingid">Total</label>
                            
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
    export default {
        props: {
            booking:{
                type: Object,
                required: true
            }
        },
        data(){
            return{
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                quantity:this.booking.quantity_of_item,
            }
        },
        methods:{
            submitForm() {
                if (this.quantity < 1 || this.quantity > this.booking.product_id.quantity) {
                    alert('Invalid quantity. Please enter a quantity within the allowed range.');
                    return;
                }
                this.reviewCart(this.booking.bookingid);
            },
            async reviewCart(bookingid){
                if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                    await axios
                    .post("http://127.0.0.1:1430/user-api/bookings/"+bookingid,{
                        quantity:this.quantity,
                    })
                    .then((response)=>response.data)
                    .then((response)=>{console.log(response)})
                    location.href="/cart"
                }else{
                    alert("Please login and try again!")
                }
            }
        }
}
</script>