package tinyhumans

import "fmt"

// TinyHumansError represents an error returned by the TinyHumans API.
type TinyHumansError struct {
	Message string
	Status  int
	Body    interface{}
}

func (e *TinyHumansError) Error() string {
	return fmt.Sprintf("TinyHumansError (status %d): %s", e.Status, e.Message)
}
