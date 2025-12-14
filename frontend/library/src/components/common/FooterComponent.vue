<template>
    <footer class="p-2">
        <div class="container">
            Inspired by <a href="https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django" target="_blank"
                rel="noopener noreferrer">Mozilla's tutorial on Django</a>
        </div>
    </footer>
</template>

<style>
    /* Footer */
    footer {
    background-color: var(--primary-color);
    color: #bdc3c7;
    padding: 1rem 0;
    text-align: center;
    font-size: 0.9rem;
    margin-top: 4rem;
    user-select: none;
    }

    footer a {
    color: var(--accent-color);
    text-decoration: none;
    font-weight: 600;
    }

    footer a:hover {
    text-decoration: underline;
    }
</style>