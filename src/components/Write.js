import { useState, useEffect, useRef } from "react";
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import InputField from './InputField';
import { useApi } from '../contexts/ApiProvider';
import { useFlash } from '../contexts/FlashProvider';
import { Link } from "react-router-dom";

export default function Write() {
    const [formErrors, setFormErrors] = useState({});
    const titleField = useRef();
    const api = useApi();
    const flash = useFlash();

    useEffect(() => {
        titleField.current.focus();
    }, []);

    const onSubmit = async (e) => {
        e.preventDefault();
        const title = titleField.current.value;

        const errors = {};
        if (!title) {
            errors.title = 'Prompt must not be empty.';
        }
        if (title.length > 140) {
            errors.title = 'Prompt cannot exceed 140 characters.';
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            return;
        }

        flash('Submitted! Please wait for ChatGPT to genereate your story.', 'info');
        const response = await api.post('/stories', {title});
        if (response.ok) {
            flash(
                <>
                    ChatGPT has responded to your prompt: <Link to={'/story/' + response.body.id} className="story-flash">{title}</Link>
                </>, 'success'
            );
        } else {
            flash(response.body.message, 'danger');
        }
    };

    return (
        <Stack direction="horizontal" gap={3} className="Write">
            <Form onSubmit={onSubmit}>
                <InputField
                    name="title" placeholder="What would you like ChatGPT to write about today?"
                    error={formErrors.title} fieldRef={titleField}
                />
                <Button variant="primary" type="submit">Write</Button>
            </Form>
        </Stack>
    )
}