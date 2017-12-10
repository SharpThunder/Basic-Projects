package com.company;

public class Main {

    public static void main(String[] args) {
	// write your code here
        Customer first = new Customer("Salad", "Ahmet");
        Waiter w = new Waiter(Customer.getMeal(),Customer.getCustomerName());
        Cook a = new Cook(Customer.getMeal(),Customer.getCustomerName());
        first.callwaiter();
        first.giveorder();
        w.getorder();
        a.makethefood();
        w.deliverorder();
        first.paybill();

        Customer second = new Customer("Main Meal", "Mehmet");
        w = new Waiter(Customer.getMeal(), Customer.getCustomerName());
        a = new Cook(Customer.getMeal(),Customer.getCustomerName());

        second.callwaiter();
        second.giveorder();
        w.getorder();
        a.makethefood();
        w.deliverorder();
        second.paybill();

        Customer third = new Customer("Salad", "Hasan");
        w = new Waiter(Customer.getMeal(), Customer.getCustomerName());
        a = new Cook(Customer.getMeal(),Customer.getCustomerName());
        third.callwaiter();
        third.giveorder();
        w.getorder();
        a.makethefood();
        w.deliverorder();
        third.paybill();




    }
}
