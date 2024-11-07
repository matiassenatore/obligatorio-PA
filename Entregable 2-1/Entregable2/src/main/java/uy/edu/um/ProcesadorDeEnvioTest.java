package uy.edu.um;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ProcesadorDeEnvioTest {

    @Test
    public void testEnviarPedido() {
        ProcesadorDeEnvio procesador = new ProcesadorDeEnvio();
        Pedido pedido = new Pedido(1, 1);
        assertDoesNotThrow(() -> procesador.enviarPedido(pedido));
    }
}
