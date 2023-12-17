<template>
    <div class="modal fade" :id="this.product.pid + 'EditProductModal'">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5">Edit Product</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editProduct(product.pid)">
                <div class="modal-body">
                    <div class="form-floating mb-3">
                        <input v-model="updated_pname" name="ProductName" value="this.product.pname" type="text" class="form-control" id="ProductName" placeholder="For Eg.: Chilli Powder" required>
                        <label for="ProductName">Product Name</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="updated_manf_date" name="manf_date" value="this.product.manf_date" type="date" class="form-control" id="manf_date" required>
                        <label for="manf_date">Manufacture Date</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="updated_exp_date" name="exp_date" value="this.product.exp_date" type="date" class="form-control" id="exp_date" required>
                        <label for="exp_date">Expiry Date</label>
                    </div>
                    <div class="form-floating mb-3">
                        <select v-model="updated_unit" name="Unit" class="form-select" value="this.product.unit" id="Unit" aria-label="Floating label select example" required>
                        <option value="kg">kg</option>
                        <option value="gm">gm</option>
                        <option value="litre">litre</option>
                        <option value="dozen">dozen</option>
                        <option value="piece">piece</option>
                        </select>
                        <label for="Unit">Unit</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="updated_rateperunit" name="Rate/unit" value="this.product.rateperunit" type="number" class="form-control" id="Rate/unit" min="1" required>
                        <label for="Rate/unit">Rate/unit</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="updated_quantity" name="Quantity" value="this.product.quantity" type="number" class="form-control" id="Quantity" min="1" required>
                        <label for="Quantity">Quantity</label>
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
            product:{
                type: Object,
                required: true
            }
        },
        data(){
            return {
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                updated_pname:this.product.pname,
                updated_manf_date:new Date(this.product.manf_date).toISOString().split('T')[0],
                updated_exp_date:new Date(this.product.exp_date).toISOString().split('T')[0],
                updated_unit:this.product.unit,
                updated_rateperunit:this.product.rateperunit,
                updated_quantity:this.product.quantity
            }
        },
        methods:{
            async editProduct(pid){
                if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                await axios
                .post("http://127.0.0.1:1430/manager-api/product/"+pid,{
                    pname:this.updated_pname,
                    manf_date:this.updated_manf_date,
                    exp_date:this.updated_exp_date,
                    unit:this.updated_unit,
                    rateperunit:this.updated_rateperunit,
                    quantity:this.updated_quantity
                })
                .then((response)=>response.data)
                .then((response)=>{
                    if (response && response.hasOwnProperty('error')){
                        alert(response['error'])
                    }else{
                        location.href="/dashboard"
                    }
                })             
            }else{alert("Please login and try again!")}
        }
    }
}
</script>