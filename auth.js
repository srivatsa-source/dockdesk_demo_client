function login(user) {
    // Current Logic: Users must be 18 or older
    if (user.age < 18) throw new Error("Adults only");
    return true;
}