package com.company;

public class Customer implements CustomerInterface  {

    private static String MealName;
    public static String CustomerName;


    public Customer(String MealName, String CustomerName) {
        this.MealName = MealName;
        this.CustomerName = CustomerName;
    }

    public static String getMeal() {
        return MealName;
    }

    public static String getCustomerName() {
        return CustomerName;
    }

    @Override
    public void callwaiter() {
        System.out.println(CustomerName + " calls waiter");

    }

    @Override
    public void giveorder() {
        System.out.println(CustomerName + " wants " + MealName + " from waiter ");

    }

    @Override
    public void paybill() {
        System.out.println(CustomerName + " paid the bill.");
    }
}
