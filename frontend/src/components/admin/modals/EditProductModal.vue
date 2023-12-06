<template>
    <div class="modal fade" :id="category.cid + 'AddProductModal'">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5">Edit Product</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method = "POST" action = "/edit/product/{{ product['pid'] }}">
                <div class="modal-body">
                    <div class="form-floating mb-3">
                        <input name="ProductName" value="{{ product['pname'] }}" type="text" class="form-control" id="ProductName" placeholder="For Eg.: Chilli Powder" required>
                        <label for="ProductName">Product Name</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input name="manf_date" value="{{ product['manf_date'] }}" type="date" class="form-control" id="manf_date" required>
                        <label for="manf_date">Manufacture Date</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input name="exp_date" value="{{ product['exp_date'] }}" type="date" class="form-control" id="exp_date" required>
                        <label for="exp_date">Expiry Date</label>
                    </div>
                    <div class="form-floating mb-3">
                        <select name="Unit" class="form-select" value="{{ product['unit'] }}" id="Unit" aria-label="Floating label select example" onchange="myFunction()" required>
                        <option value="kg">kg</option>
                        <option value="gm">gm</option>
                        <option value="litre">litre</option>
                        <option value="dozen">dozen</option>
                        <option value="piece">piece</option>
                        </select>
                        <label for="Unit">Unit</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input name="Rate/unit" value="{{ product['rateperunit'] }}" type="number" class="form-control" id="Rate/unit" min="1" required>
                        <label for="Rate/unit">Rate/unit</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input name="Quantity" value="{{ product['quantity'] }}" type="number" class="form-control" id="Quantity" min="1" required>
                        <label for="Quantity">Quantity</label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save changes</button>
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
            category:{
                type: Object,
                required: true
            }
        }
    }
</script>