<template>
    <div class="modal fade" id="{{ product['pid'] }}AddToCartModal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add To Cart: {{ product['pname'] }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form method = "POST" action = "/create/bookings/{{ category['cid'] }}/{{ product['pid'] }}">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input type="text" class="form-control" value='In Stock' id="Availability" readonly>
                            <label for="Availability">Availability</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input type="number" class="form-control" id="Quantity{{ product['pid'] }}" name="Quantity" min="1" max="{{ product['quantity'] }}" oninput="calculateTotal{{ product['pid'] }}()">
                            <label for="Quantity{{ product['pid'] }}">Quantity</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input type="number" class="form-control" value="{{ product['rateperunit'] }}" id="Price{{ product['pid'] }}" readonly>
                            <label for="Price{{ product['pid'] }}">Price</label>
                        </div>
                        <div class="form-floating mb-3">
                            <input type="number" name="Total" class="form-control" value="" id="Total{{ product['pid'] }}" readonly>
                            <label for="Total{{ product['pid'] }}">Total</label>
                            
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
        }
}
</script>