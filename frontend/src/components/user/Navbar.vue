<template>
    <nav class="navbar navbar-expand-lg bg-dark sticky-top bg-gradient">
        <div class="container">
            <a class="navbar-brand" href="/" style="font-family: 'Bagel Fat One';font-size: 32px; color: aliceblue;">Grocilla ;)</a>
            <span class="navbar-text" style="font-size: 28px; color: aliceblue;">welcomes you, User!</span>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <div class="navbar-nav ms-auto mb-2 mb-lg-0 gap-2">
                    <a href="/cart" class="btn btn-outline-light" style="margin-left: 5px">My Cart</a>
                    <a href="/orders" class="btn btn-outline-light" style="margin-left: 5px">My Orders</a>
                    <a href="/logout" class="btn btn-outline-light" style="margin-left: 5px">Logout</a>
                </div>
            </div>
        </div>
    </nav>
</template>