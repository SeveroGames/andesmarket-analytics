-- 1. Vista de Rendimiento de Productos (Window Function: RANK y PARTITION BY)
-- KPI: Top productos por categoría según sus ingresos.
CREATE OR REPLACE VIEW vw_product_performance AS
WITH ProductSales AS (
    SELECT 
        c.categoria,
        p.nombre_producto,
        SUM(v.cantidad) AS total_unidades_vendidas,
        SUM(v.cantidad * p.precio_unitario) AS ingresos_totales
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto
    JOIN categorias c ON p.id_categoria = c.id_categoria
    WHERE v.estado = 'Completa'
    GROUP BY c.categoria, p.nombre_producto
)
SELECT 
    categoria,
    nombre_producto,
    total_unidades_vendidas,
    ingresos_totales,
    RANK() OVER(PARTITION BY categoria ORDER BY ingresos_totales DESC) AS ranking_ingresos
FROM ProductSales;


-- 2. Vista de Crecimiento Mensual (Window Function: LAG)
-- KPI: Month-over-Month (MoM) Growth. Compara los ingresos de un mes con el mes anterior.
CREATE OR REPLACE VIEW vw_monthly_sales_growth AS
WITH VentasMensuales AS (
    SELECT 
        DATE_TRUNC('month', v.fecha) AS mes,
        SUM(v.cantidad) AS unidades_vendidas,
        SUM(v.cantidad * p.precio_unitario) AS ingresos_totales
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto
    WHERE v.estado = 'Completa'
    GROUP BY DATE_TRUNC('month', v.fecha)
)
SELECT 
    mes,
    unidades_vendidas,
    ingresos_totales,
    LAG(ingresos_totales, 1) OVER(ORDER BY mes) AS ingresos_mes_anterior,
    ROUND(
        ((ingresos_totales - LAG(ingresos_totales, 1) OVER(ORDER BY mes)) / 
        NULLIF(LAG(ingresos_totales, 1) OVER(ORDER BY mes), 0)) * 100, 
    2) AS crecimiento_porcentual
FROM VentasMensuales;


-- 3. Vista de Preparación para RFM (Agregaciones complejas)
-- Nos prepara los datos base para el modelo de Machine Learning de la Fase 8
CREATE OR REPLACE VIEW vw_customer_rfm_prep AS
SELECT 
    c.id_cliente,
    c.nombre,
    c.apellido,
    MAX(v.fecha) AS ultima_compra,
    -- Recency: Días desde su última compra hasta hoy
    EXTRACT(DAY FROM (CURRENT_TIMESTAMP - MAX(v.fecha))) AS recency_dias,
    -- Frequency: Cantidad de compras distintas
    COUNT(DISTINCT v.id_venta) AS frequency,
    -- Monetary: Cuánto dinero ha gastado en total
    SUM(v.cantidad * p.precio_unitario) AS monetary
FROM clientes c
JOIN ventas v ON c.id_cliente = v.id_cliente
JOIN productos p ON v.id_producto = p.id_producto
WHERE v.estado = 'Completa'
GROUP BY c.id_cliente, c.nombre, c.apellido;