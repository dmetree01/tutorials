/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { todoPropShape, Todo } from "../todo";

export class TodoList extends Component {
    static template = "owl_playground.todo-list";
    static components = { Todo };
    static props = { todos: {type: Array, element: todoPropShape} };
    
    todos = useState(this.props.todos)
    inputRef = useRef("todoInput");

    setup() {
        onMounted(() => {
            this.focusInput()
        })
    }

    focusInput() {
        this.inputRef.el.focus();
    }

    toggleState(e) {
        const todo = this.todos.find(it => it.id == e.target.value)
        todo.done = !todo.done;
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value?.length) {
            this.todos.push({
                id: (Math.max(...(this.todos.map(it => it.id)), 0)+1),
                description: e.target.value,
                done: false,
            });
        }
    }

    removeTodo(e) {
        const index = this.todos.findIndex((it) => it.id == e.target.getAttribute('data-id'));
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
