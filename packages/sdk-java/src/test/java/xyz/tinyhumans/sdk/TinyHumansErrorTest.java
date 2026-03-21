package xyz.tinyhumans.sdk;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class TinyHumansErrorTest {

    @Test
    void constructorSetsFields() {
        TinyHumansError err = new TinyHumansError("bad request", 400, Map.of("error", "bad"));
        assertEquals("bad request", err.getMessage());
        assertEquals(400, err.getStatus());
        assertEquals(Map.of("error", "bad"), err.getBody());
    }

    @Test
    void constructorWithoutBody() {
        TinyHumansError err = new TinyHumansError("not found", 404);
        assertEquals("not found", err.getMessage());
        assertEquals(404, err.getStatus());
        assertNull(err.getBody());
    }

    @Test
    void isRuntimeException() {
        TinyHumansError err = new TinyHumansError("fail", 500);
        assertInstanceOf(RuntimeException.class, err);
    }
}
