function login(user) {
    // Changing logic back to 18 to see if bot notices both files
    if (user.age < 18) throw new Error("Adults only");
    return true;
}
