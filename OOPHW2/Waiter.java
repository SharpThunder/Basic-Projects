package com.company;

public class Waiter implements WaiterInterface {
    public String MealName;
    public String CustomerName;
    public Waiter(String MealName, String CustomerName) {
        this.CustomerName = CustomerName;
        this.MealName = MealName;

    }

    @Override
    public void getorder() {
        System.out.println(CustomerName+ "'s  order " + MealName + " get by waiter");


    }

    @Override
    public void deliverorder() {
        System.out.println(MealName + " delivered to  " + CustomerName);

    }
}
