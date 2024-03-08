with customers as (
    select id,
           first_name,
           last_name
    from `dbt-tutorial`.jaffle_shop.customers
),

orders as (
    select id,
           user_id,
           order_date,
           status
    from `dbt-tutorial`.jaffle_shop.orders
),

customer_orders as (
    SELECT
        user_id,
        min(order_date) as first_order,
        max(order_date) as most_recent_order,
        count(id) as number_of_orders
    from orders
    group by user_id
),

final as (
    select
        customers.id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order,
        customer_orders.most_recent_order,
        customer_orders.number_of_orders
    from customers
    left join  customer_orders
    on customers.id = customer_orders.user_id
)

select * from final