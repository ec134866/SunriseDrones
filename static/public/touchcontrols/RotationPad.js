import * as utils from './utils.js'


class RotationPad {
    container
    padElement
    region
    handle
    eventRepeatTimeout
    regionData = {}
    handleData = {}
    mouseDown = false
    mouseStopped = false

    constructor(container) {
        this.container = container
        this.padElement = document.createElement('div')
        this.padElement.classList.add('rotation-pad')
        this.region = document.createElement('div')
        this.region.classList.add('region')
        this.handle = document.createElement('div')
        this.handle.classList.add('handle')
        this.region.appendChild(this.handle)
        this.padElement.append(this.region)
        this.container.append(this.padElement)

        this.container.style.position = 'relative';

        // Aligning pad:
        let canvas = container.getElementsByTagName('canvas')[0]
        this.alignAndConfigPad(canvas)

        // events
        window.addEventListener('resize', () => {this.alignAndConfigPad(canvas)})

        // Mouse events:
        this.region.addEventListener('mousedown', (event) => {
            this.mouseDown = true
            this.handle.style.opacity = 1.0
            this.update(event.pageX, event.pageY)
        })

        document.addEventListener('mouseup', () => {
            this.mouseDown = false
            this.resetHandlePosition()
        })

        document.addEventListener('mousemove', (event) => {
            if (!this.mouseDown)
                return
            this.update(event.pageX, event.pageY)
        })

        //Touch events:
        this.region.addEventListener('touchstart', (event) => {
            event.preventDefault();
            this.mouseDown = true
            this.handle.style.opacity = 1.0
            this.update(
                event.targetTouches[0].pageX,
                event.targetTouches[0].pageY
            )
        },{ passive: false }); 

        let touchEnd = () => {
            this.mouseDown = false
            this.resetHandlePosition()
        }
        document.addEventListener('touchend', touchEnd,{ passive: false }); 
        document.addEventListener('touchcancel', touchEnd,{ passive: false }); 

        document.addEventListener('touchmove', (event) => {
            if (!this.mouseDown)
                return
            event.preventDefault();
            this.update(event.touches[0].pageX, event.touches[0].pageY)
        },{ passive: false }); 

        this.resetHandlePosition()
    }

    alignAndConfigPad(canvas){
        const containerRect = this.container.getBoundingClientRect();

        this.padElement.style.position = 'absolute';

        // Adjusting the height and width as per your requirement
        // const padWidth = this.region.offsetWidth * 0.75; 
        // const padHeight = this.region.offsetHeight * 0.55; 

        const aspectRatio = canvas.width / canvas.height;  // Assuming canvas is the image element.
    
        // Set the height to your desired height
        const padHeight = containerRect.height * 0.55;

        // Calculate the width based on the aspect ratio
        const padWidth = padHeight * aspectRatio;

        this.region.style.width = `${padWidth}px`;
        this.region.style.height = `${padHeight}px`;

        // this.region.offsetHeight = height of the image (100)
    
        const verticalOffset = (window.innerHeight * 0.75) - this.region.offsetHeight;
        const horizontalOffset = (containerRect.width * 0.95) - this.region.offsetWidth; 

        this.padElement.style.top = `${verticalOffset}px`;
        this.padElement.style.left = `${horizontalOffset}px`;

        // console.log("Current Container:");
        // console.log("Container ID:", this.container.id); 
        // console.log("Container Type:", this.container.tagName);


        // console.log("Container Dimensions and Position:");
        // console.log("Width:", containerRect.width);
        // console.log("Height:", containerRect.height);
        // console.log("Top:", containerRect.top);
        // console.log("Right:", containerRect.right);
        // console.log("Bottom:", containerRect.bottom);
        // console.log("Left:", containerRect.left);

        // // Log canvas dimensions
        // console.log("Canvas Dimensions:");
        // console.log("Offset Width:", canvas.offsetWidth);
        // console.log("Width:", canvas.width);
        // console.log("Offset Height:", canvas.offsetHeight);
        // console.log("Height:", canvas.height);

        // console.log("Region Dimensions:");
        // console.log("Width:", this.region.offsetWidth);
        // console.log("Height:", this.region.offsetHeight);

        // console.log("Calculating Pad Position:");
        // console.log(`Vertical Offset Calculation: (${window.innerHeight * 0.75}) - (${this.region.offsetHeight}) = ${verticalOffset}`);
        // console.log(`Horizontal Offset Calculation: (${containerRect.width} * 0.95) - (${this.region.offsetWidth}) = ${horizontalOffset}`);

        // console.log("Pad Position:");
        // console.log("Top:", this.padElement.style.top);
        // console.log("Left:", this.padElement.style.left);


        this.regionData.width = this.region.offsetWidth;
        this.regionData.height = this.region.offsetHeight;
        this.regionData.position = {
            top: this.region.offsetTop,
            left: this.region.offsetLeft
        };
        this.regionData.offset = utils.getOffset(this.region);
        this.regionData.radius = this.regionData.width / 2;
        this.regionData.centerX = this.regionData.position.left + this.regionData.radius;
        this.regionData.centerY = this.regionData.position.top + this.regionData.radius;

        this.handleData.width = this.handle.offsetWidth;
        this.handleData.height = this.handle.offsetHeight;
        this.handleData.radius = this.handleData.width / 2;

        this.regionData.radius = this.regionData.width / 2 - this.handleData.radius;
    }

    update(pageX, pageY) {
        let newLeft = pageX - this.regionData.offset.left;
        let newTop = pageY - this.regionData.offset.top;
    
        // Clamping handle within circular region
        let dx = newLeft - this.regionData.centerX;
        let dy = newTop - this.regionData.centerY;
        let distance = Math.sqrt(dx * dx + dy * dy);
    
        if (distance > this.regionData.radius) {
            let angle = Math.atan2(dy, dx);
            newLeft = this.regionData.centerX + Math.cos(angle) * this.regionData.radius;
            newTop = this.regionData.centerY + Math.sin(angle) * this.regionData.radius;
        }
    
        // Update the handle's position
        newTop = Math.round(newTop * 10) / 10;
        newLeft = this.regionData.centerX;
    
        this.handle.style.top = `${newTop - this.handleData.radius}px`;
        this.handle.style.left = `${newLeft - this.handleData.radius}px`;
    
        // Calculate deltaY (vertical movement)
        let deltaY = this.regionData.centerY - newTop;
        this.sendEvent(0, deltaY);  // Send only vertical movement event
    }

    sendEvent(dx, dy) {
        if (this.eventRepeatTimeout) {
            clearTimeout(this.eventRepeatTimeout)
        }

        if (!this.mouseDown) {
            clearTimeout(this.eventRepeatTimeout)
            return
        }

        this.eventRepeatTimeout = setTimeout(() => {
            this.sendEvent(dx, dy)
        }, 5)

        let moveEvent = new CustomEvent('move', {
            bubbles: false,
            detail: {
                'deltaX': dx,
                'deltaY': dy
            }
        })
        this.padElement.dispatchEvent(moveEvent)
    }

    resetHandlePosition() {
        this.handle.style.top = this.regionData.centerY - this.handleData.radius + 'px'
        this.handle.style.left = this.regionData.centerX - this.handleData.radius + 'px'
        this.handle.style.opacity = 0.1
    }
}


export default RotationPad
