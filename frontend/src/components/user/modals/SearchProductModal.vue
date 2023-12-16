<template>
    <div class="modal fade" id="SearchProductModal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Search Product</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form method = "POST" action = "/search_product">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input name="product" type="search" class="form-control" id="product" list="search product" placeholder="For Eg.: Apple" required>
                            <datalist id="search product">
                                
                                <!-- <option value="{{ product.pname'] }}"> -->
                                
                            </datalist> 
                            <label for="product">Product Name</label> 
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Search</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
    export default {
        
}
</script>