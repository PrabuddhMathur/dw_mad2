<template>
    <div class="modal fade" :id="product.pid +'AddToCartModal'">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add To Cart: {{ product.pname }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="submitForm">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input type="text" class="form-control" value='In Stock' id="Availability" readonly>
                            <label for="Availability">Availability</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input v-model="quantity" type="number" class="form-control" :id="'Quantity'+ product.pid" name="Quantity" :min="1" :max=product.quantity>
                            <label :for="'Quantity'+ product.pid">Quantity</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input type="number" class="form-control" :value="product.rateperunit" :id="'Price'+product.pid" readonly>
                            <label :for="'Price'+product.pid">Price</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input type="number" name="Total" class="form-control" :value="quantity*product.rateperunit" :id="'Total'+product.pid" readonly>
                            <label :for="'Total'+product.pid">Total</label>
                            
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
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
            product:{
                type: Object,
                required: true
            },
            category_name:{
                type:String,
                required:true
            }
        },
        data(){
            return{
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                quantity:'',
            }
        },
        methods:{
            submitForm() {
                if (this.quantity < 1 || this.quantity > this.product.quantity) {
                    alert('Invalid quantity. Please enter a quantity within the allowed range.');
                    return;
                }
                this.addtoCart(this.product.pid);
            },
            async addtoCart(pid){
                if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                    await axios
                    .post("http://127.0.0.1:1430/user-api/bookings/"+pid,{
                        quantity:this.quantity,
                        product_name:this.product.pname,
                        category_name:this.category_name,
                        pid:this.product.pid,
                    })
                    .then((response)=>response.data)
                    .then((response)=>{console.log(response)})
                    this.$router.push("/cart")
                }else{
                    alert("Please login and try again!")
                }
            }
        }
}
</script>