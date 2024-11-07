package uy.edu.um;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ProcesadorDePedidosTest {

    @Test
    public void testProcesamientoDePedido() {
        Pedido pedido = new Pedido(1, 1);
        assertDoesNotThrow(() -> {
            ProcesadorDePedidos procesador = new ProcesadorDePedidos(10);
            procesador.agregarPedido(pedido); // Cambié agregarPedidos() por agregarPedido() si estamos agregando uno.

            procesador.procesarPedidos();

            // Espera para asegurarse de que los pedidos se procesen antes de finalizar el test
            procesador.shutdown();
            procesador.esperarTerminacion();  // Llama al nuevo método encapsulado
        });
    }

    @Test
    public void testShutdown() {
        ProcesadorDePedidos procesador = new ProcesadorDePedidos(10);
        procesador.shutdown();
        assertTrue(procesador.isShutdown());
    }
}
