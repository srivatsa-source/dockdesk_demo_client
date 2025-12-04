function login(user) {
    if (user.age < 18) {
        throw new Error("User must be 18 or older.");
    }
    return true;
}