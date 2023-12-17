<template>
    <div class="modal fade" id="SearchProductModal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Search Product</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="searchProducts">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input v-model="product" type="search" class="form-control" id="product" list="search product" placeholder="For Eg.: Apple" required>
                            <datalist id="search product">
                                <span v-for="product in products"  :key="product.pid">
                                    <option :value="product.pname" />
                                </span>
                            </datalist> 
                            <label for="product">Product Name</label> 
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Search</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            products:{
                type:Object,
                required:true
            }
        },
        data(){
            return{
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                product:'',
            }
        },
        methods:{
            async searchProducts(){
                if (this.userSession){
                    this.$router.push({name:"search",query:{search_by:'product',q:this.product}})
                }else{
                    alert("Please login and try again!")
                }
            }
        }
}
</script>